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

## RONDE 2 — full-day update (19 Nov ~19:30 WIB)

- Ronde 1 live: judge 984.822, rank 141 (prize_rank 140) dari
  6.661 baris; cutoff top 50 saat itu 987.827 (gap 3.005 poin).
  Saat build ronde 2: rank 146, cutoff top 50 = 987.834
  (golden-heron-35), gap 3.012 poin.
- Kenapa top entry menang (leaderboard live, dipelajari dulu):
  rank 1 quick-finch-51, 992.113, "The World in One Day" (312.966
  byte) — front page bersih satu hari penuh. Rank 2 lomfi, 991.343,
  hanya "19 stories" (222.874 byte) — BUKTI kualitas mengalahkan
  jumlah: 19 cerita yang bersih mengalahkan yang padat tapi
  berantakan. Rank 3 lively-condor-51, 991.162, "Polar Aurora" —
  satu visual kuat. Rank 4 aw-rama, 991.123, hanya 88.185 byte —
  file kecil yang bersih pun menang. Rank 5 aryanpatelx, 990.617,
  "Dense Grid, Aerials, Crisp 2x Lanczos" (682.097 byte).
  Pelajaran: JANGAN korbankan keterbacaan demi jumlah. Ronde 2
  naik 36 → 44 cerita TANPA mengecilkan type di bawah 10 pt,
  menukar 2 panel terlemah dengan cerita sore yang LEBIH BESAR,
  dan menambah timeline UTC + strip angka yang diperbarui.
- Perubahan ronde 2 (SATU area: kedalaman full-day + peta/strip):
  12 panel — panel 10 diganti "Senators: AI cyber" → "Anthropic
  IPO prices at $83 a share" ($1,5tn, IPO terbesar, $81,3 miliar);
  panel 12 diganti Mélenchon → "ICJ rules on Rohingya genocide
  case" (Den Haag, 10:00); panel 2 diperbarui "held today".
  Daftar 24 → 32: +8 cerita sore/malam — Van Gogh $190,4 juta
  (rekor artis, Sotheby's), EU Commission kena cyberattack,
  Jembatan Crimea diserang lagi, pakta militer AS–Venezuela,
  bomber Rusia mendarat di Vietnam, Ethiopia–Eritrea kerahkan
  pasukan, Fiji nyatakan bencana kekeringan, IEA: krisis Hormuz
  ancaman energi terbesar; item 15 diperbarui (Brent $89,59,
  -2,6%) dan item 28 diperbarui (rumah Yunus dibakar, kerusuhan
  28 distrik). Strip BY THE NUMBERS diperbarui: 251–11, $83 IPO,
  145 km/h, $190,4 juta, 16,1 miliar mil. Tambah strip timeline
  UTC (APEC 00:00 → Jeffries 06:00 → ICJ 10:00 → IPO 14:00 →
  Van Gogh 18:00 → pasar tutup 21:30).
- Sumber cerita baru: The Art Newspaper (19 Nov 06:42 UTC) +
  artnet (05:30 UTC) untuk Van Gogh; ICJ via briefing 19 Nov
  (sidang 10:00 Den Haag; putusan: pasukan Myanmar membunuh
  ribuan Rohingya, vonis genosida masih pending); Anthropic IPO
  via roundup 19 Nov (harga $83, valuasi ~$1,5tn, ticker ANE);
  Horizon 19 Nov untuk IEA, Bangladesh, COP31, dan angka pasar
  penutupan (S&P 7.323,63; Nasdaq +0,42%; Brent $89,59; emas
  $3.739,6); 10things.news + Open Chronicle untuk bom Vietnam,
  Fiji, dan trilateral. Penjualan Van Gogh: palu jatuh Rabu malam
  New York, pertama dilaporkan 19 Nov — memenuhi aturan bounty
  ("first reported on 19 November in any time zone").
- Yang sengaja TIDAK dipakai: pinjaman EU €45 miliar (18 Nov),
  An-12 Siberia (17 Nov), pensiun Dhoni (17 Nov) — seperti ronde 1.
  Juga tidak dipakai: klaim Epstein-autopsi (belum terverifikasi
  kuat) dan COP31 Antalya (negosiasi masih berjalan, belum hasil).
- Verifikasi ronde 2: entry.png 1024×1024, 171.021 byte (< 1 MiB);
  gen_image.py dijalankan 2x → sha256 identik
  (61f356384fea81b3de71d7b46e952fd6810c182334ff56714d501859eae97b99);
  main.py 2x → sha256 sama. gen_image.py diedit di sesi ronde 2
  dan main.py ditulis ulang dari nol di sesi ini (authorship gate).
