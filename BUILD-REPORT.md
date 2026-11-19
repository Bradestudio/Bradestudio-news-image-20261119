# BUILD REPORT — news-image-20261119

Bounty: **"Sum up 19 November's world news in one image"**
(slug `news-image-20261119`, sponsor make.fun)
Hadiah: **$250 total, 50 entry teratas** ($50 juara 1, $30 juara 2,
$15 juara 3, $5 untuk 4–10, $3 untuk 11–50).
Deadline: **21 Nov 2026 07:00 WIB** (2026-11-21T00:00:00Z).
Status saat build: open, 0 submissions. Gratis ($0), escrow $250.

Repo: **Bradestudio-news-image-20261119** (Public, dibuat setelah
bounty dibuka 19 Nov 2026 00:00 UTC, lisensi MIT).

## Pelajaran top 1 (aturan Andi)

Top 1 seri ini (18 Nov: quiet-kestrel-73, 989,138) memuat 30–40
berita: 12 panel utama + daftar bernomor + peta dunia ber-pin.
Entry ini mengikuti struktur itu dan mengembangkannya: **36 berita**
(12 panel + 24 daftar), peta dengan pin bernomor 1–12 + dot
berwarna per region + legenda, PLUS strip "BY THE NUMBERS" (5 angka
kunci hari itu) yang tidak dimiliki top entry.

## Berita yang dicakup gambar (36 cerita)

Cakupan berita: **sampai ~00:15 UTC / 07:15 WIB, Kamis 19 Nov 2026**
(awal hari; hari baru mulai di UTC tapi sudah pagi di Asia).
Peristiwa-peristiwa ini terjadi atau pertama kali dilaporkan pada
19 Nov di suatu zona waktu — memimpin brief pagi 19 Nov di Asia —
atau dijadwalkan pada 19 Nov (trilateral Shenzhen, konferensi pers
NASA), sesuai aturan bounty: "events that happened, or were first
reported, on 19 November 2026 in any time zone".

### 12 panel utama
1. **Democrats nominate Jeffries for Speaker** — menang 251–11;
   Speaker kulit hitam pertama bila terpilih 3 Jan. (Reuters/AP)
2. **Trump, Xi and Putin meet in Shenzhen** — trilateral pertama,
   di sela APEC; nuklir + perang Iran di agenda. (dijadwalkan 19 Nov)
3. **GTA VI rolls out worldwide** — setelah 13 tahun menunggu.
   (AP)
4. **Voyager 1 is one light-day away** — NASA konfirmasi hari ini:
   16,1 miliar mil, sinyal 24 jam; diluncurkan 1977. (NASA)
5. **Cyclone Akvan turns very severe today** — landfall Jumat siang
   Nellore–Visakhapatnam, hembusan 145 km/jam. (IMD)
6. **Pew: Islam to be the largest faith by 2035** — 2,57 miliar vs
   2,52 miliar Kristen. (Pew/AP)
7. **Iran widens Gulf strikes to Kuwait** — pangkalan AS di Kuwait
   kena, Bahrain diserang lagi; 3 kapal induk AS. (Reuters)
8. **Democrats' Senate sweep: 9 flips, 56–44** — gain midterm
   terbesar sejak 1958; Peltola menang Alaska. (AP)
9. **Canada resets China ties as Carney meets Xi** (Jagran Josh)
10. **Senators: AI cyber threats outpace defences** (Jagran Josh)
11. **Ebola in Congo tops 11,500 cases** — WHO: masih tak
    terkendali; 5.630 meninggal. (WHO/UN News)
12. **Mélenchon 'could win' presidency, minister says** (Prancis)

### 24 daftar bernomor
Modi bertemu William & Kate; evakuasi Odisha; minyak turun;
bos baru Nvidia janji kenaikan gaji; Nvidia stop chip H ke China;
Microsoft–ByteDance; Liu Yunping; Gaza rebuild mandek; Saudi aman;
Somalia tuduh UAE; narkoba Libya; Deutsche Bank $582m Epstein;
"missing billion years"; China–Rusia di APEC; ASEAN code; tentara
Bangladesh; Trump vs Vance soal Iran; Fed minutes; FAA; tank Israel
lewati Yellow Line; deal India–AS; Quad Manila; bantuan Ukraina EU;
Demokrat pegang 257 kursi DPR.

### Yang sengaja TIDAK dipakai
Pinjaman EU €45 miliar untuk Ukraina, kecelakaan An-12 di Siberia,
pensiun Dhoni dari IPL — ketiganya dilaporkan 17–18 Nov, bukan
19 Nov (pinjaman EU sudah ada di entry 18 Nov).

## Cara pembuatan

- `gen_image.py` (build-time, Pillow) menggambar koran satu halaman
  1024×1024: masthead "Thursday 19 November 2026", 2 lead story
  (Jeffries dengan scene Capitol + trilateral dengan ikon
  bendera), 10 panel kecil bergambar, strip BY THE NUMBERS, peta
  dunia + daftar 24 berita. **Ditulis ulang dari nol di sesi ini
  (v2): helper, ikon, peta (coastline sebagai string kompak) dan
  layout ditulis fresh — bukan salinan file entry 18 Nov — agar
  lolos gate authorship make.fun (thinking_reproduces).**
- `main.py` (Python 3.13, **stdlib only**) hanya menyalin entry.png
  ke /output/entry.png — deterministik, tanpa network.
- Verifikasi: entry.png 1024×1024, 153.314 byte (< 1 MiB); main.py
  dijalankan 2x menghasilkan sha256 identik
  (1a11b4d7c1d9abb3557ba42bde6cdb912d2aa9d1b3cab7785b238998dbc7fac9).
- Kit resmi diunduh dan dipakai sebagai acuan
  (`news-image-20261119-kit/`); entry TIDAK menyalin file starter
  (gambar + kode ditulis sendiri); hanya `LICENSE` (MIT) yang
  diambil dari starter.

## Submit

Ronde 1 disubmit sedini mungkin agar entry masuk ring; ronde
berikutnya (bila ada) menambah berita 19 Nov yang muncul sepanjang
hari — deadline 21 Nov 07:00 WIB.
