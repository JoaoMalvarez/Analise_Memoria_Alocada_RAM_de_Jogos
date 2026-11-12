import psutil, time, csv, platform, argparse

IS_WIN = platform.system() == "Windows"
MB = 1024 * 1024

def find_procs(name):
    return [p for p in psutil.process_iter(["name"])
            if p.info["name"] and p.info["name"].lower() == name.lower()]

def read_proc(p):
    """Retorna (virtual, resident, pico_virtual, pico_resident) em bytes."""
    mi = p.memory_info()
    if IS_WIN:
        return mi.vms, mi.rss, mi.peak_pagefile, mi.peak_wset
    # Linux: lê os picos do /proc
    peak_v = peak_r = 0
    with open(f"/proc/{p.pid}/status") as f:
        for line in f:
            if line.startswith("VmPeak:"):
                peak_v = int(line.split()[1]) * 1024
            elif line.startswith("VmHWM:"):
                peak_r = int(line.split()[1]) * 1024
    return mi.vms, mi.rss, peak_v, peak_r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("process", help="nome do executável, ex: game.exe")
    ap.add_argument("--duration", type=int, default=600, help="segundos")
    ap.add_argument("--interval", type=float, default=1.0)
    ap.add_argument("--out", default="medicao.csv")
    a = ap.parse_args()

    procs = find_procs(a.process)
    if not procs:
        raise SystemExit(f"Processo '{a.process}' não encontrado.")

    max_virt = max_res = 0
    peak_virt_os = peak_res_os = 0
    t0 = time.time()

    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s", "virtual_MB", "residente_MB",
                    "pico_virtual_SO_MB", "pico_residente_SO_MB"])
        while time.time() - t0 < a.duration:
            v = r = pv = pr = 0
            for p in procs:
                try:
                    a_v, a_r, a_pv, a_pr = read_proc(p)
                    v += a_v; r += a_r; pv += a_pv; pr += a_pr
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            max_virt, max_res = max(max_virt, v), max(max_res, r)
            peak_virt_os, peak_res_os = max(peak_virt_os, pv), max(peak_res_os, pr)
            w.writerow([round(time.time() - t0, 1), v // MB, r // MB,
                        pv // MB, pr // MB])
            f.flush()
            time.sleep(a.interval)

    print(f"Pico virtual (amostrado):   {max_virt // MB} MB")
    print(f"Pico residente (amostrado): {max_res // MB} MB")
    print(f"Pico virtual (reportado pelo SO):   {peak_virt_os // MB} MB")
    print(f"Pico residente (reportado pelo SO): {peak_res_os // MB} MB")

if __name__ == "__main__":
    main()