"""
Medição de memória de um jogo no macOS.

Uso:
    python3 medir_mac.py NOME_DO_PROCESSO --duration 600 --out jogo_pcMac_teste1.csv

Colunas do CSV (valores em MB):
    t_s                 tempo desde o início da medição
    virtual_MB          memória virtual (vms). No macOS costuma ser MUITO grande
                        (centenas de GB) por causa de regiões reservadas pelo
                        sistema; NÃO é comparável com o "commit" do Windows.
    residente_MB        memória residente em RAM (rss)
    footprint_MB        phys_footprint: é o valor "Memória" do Monitor de Atividade
                        e a melhor medida de "memória realmente usada" no macOS
    pico_footprint_SO_MB pico de footprint desde que o processo abriu (reportado
                        pelo macOS); fica vazio (0) se o sistema não fornecer
"""
import argparse
import csv
import ctypes
import ctypes.util
import platform
import time

import psutil

MB = 1024 * 1024

if platform.system() != "Darwin":
    raise SystemExit("Este script é só para macOS. No Windows use o medir.py.")


def load_libproc():
    try:
        path = ctypes.util.find_library("proc") or "/usr/lib/libproc.dylib"
        lib = ctypes.CDLL(path)
        lib.proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
        lib.proc_pid_rusage.restype = ctypes.c_int
        return lib
    except Exception:
        return None


LIBPROC = load_libproc()
RUSAGE_INFO_V4 = 4


def footprint_info(pid):
    """Retorna (phys_footprint, pico_footprint) em bytes, ou (0, 0) se indisponível."""
    if LIBPROC is None:
        return 0, 0
    buf = (ctypes.c_uint64 * 64)()
    try:
        if LIBPROC.proc_pid_rusage(pid, RUSAGE_INFO_V4, ctypes.byref(buf)) != 0:
            return 0, 0
    except Exception:
        return 0, 0
    # Os 16 primeiros bytes são o UUID (2 slots de 64 bits).
    # phys_footprint é o 8º campo seguinte; lifetime_max_phys_footprint é o 29º.
    return int(buf[2 + 7]), int(buf[2 + 28])


def find_procs(name):
    name = name.lower()
    exact, partial = [], []
    for p in psutil.process_iter(["name"]):
        n = (p.info["name"] or "").lower()
        if n == name:
            exact.append(p)
        elif name in n:
            partial.append(p)
    return exact or partial


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("process", help="nome do processo do jogo (como aparece no Monitor de Atividade)")
    ap.add_argument("--duration", type=int, default=600, help="segundos")
    ap.add_argument("--interval", type=float, default=1.0)
    ap.add_argument("--out", default="medicao_mac.csv")
    a = ap.parse_args()

    procs = find_procs(a.process)
    if not procs:
        raise SystemExit(
            f"Processo '{a.process}' não encontrado. Confira o nome no Monitor de Atividade."
        )
    print("Processos medidos:")
    for p in procs:
        print(f"  PID {p.pid}: {p.info['name']}")

    max_virt = max_res = max_fp = 0
    peak_fp_os = 0
    t0 = time.time()

    try:
        with open(a.out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["t_s", "virtual_MB", "residente_MB",
                        "footprint_MB", "pico_footprint_SO_MB"])
            while time.time() - t0 < a.duration:
                v = r = fp = pk = 0
                for p in procs:
                    try:
                        mi = p.memory_info()
                        v += mi.vms
                        r += mi.rss
                        a_fp, a_pk = footprint_info(p.pid)
                        fp += a_fp
                        pk += a_pk
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                max_virt = max(max_virt, v)
                max_res = max(max_res, r)
                max_fp = max(max_fp, fp)
                peak_fp_os = max(peak_fp_os, pk)
                w.writerow([round(time.time() - t0, 1), v // MB, r // MB,
                            fp // MB, pk // MB])
                f.flush()
                time.sleep(a.interval)
    except KeyboardInterrupt:
        print("\nMedição interrompida (Ctrl+C). O CSV foi salvo até aqui.")

    print(f"\nVirtual máximo (amostrado):    {max_virt // MB} MB")
    print(f"Residente máximo (amostrado):  {max_res // MB} MB")
    print(f"Footprint máximo (amostrado):  {max_fp // MB} MB")
    print(f"Pico de footprint (macOS):     {peak_fp_os // MB} MB")
    print(f"Arquivo salvo: {a.out}")


if __name__ == "__main__":
    main()
