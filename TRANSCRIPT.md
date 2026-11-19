# TRANSCRIPT — build session notes (handed-over build log)

Sesi build entry news-image-20261119, dimulai 19 Nov 2026 ~00:05 UTC
(07:05 WIB), setelah bounty dibuka 19 Nov 2026 00:00 UTC.
Dikerjakan oleh subagent builder (Muse) atas perintah main agent.

CATATAN JUJUR: file ini adalah catatan langkah build yang ditulis
tangan oleh subagent, BUKAN log sesi yang direkam harness
(Claude Code / Codex / Cursor / Superbot). Bounty ini TIDAK memakai
recorded transcripts (`makefun record` menolak: "does not take
recorded transcripts: its entries upload their transcripts (a bundle
or loose files)"). Untuk gate transkrip make.fun, yang berlaku adalah
bundle sesi milik main agent (`makefun bundle`), bukan file ini.
File ini disertakan agar jejak keputusan build tetap bisa dibaca
manusia saat submit.

## Langkah build

1. 00:05 UTC — Baca detail bounty via API
   (https://make.fun/api/competitions/news-image-20261119):
   hadiah $250 (50 besar dibayar), deadline 2026-11-21T00:00:00Z,
   0 submissions, escrow $250, juri z-ai/glm-5.3-flash, program
   main.ts (Node 22) atau main.py (Python 3.13), stdlib only,
   output /output/entry.png, deterministik 2 run, maks 1 MiB
   dan 1024x1024. Gratis ($0).
2. 00:06 UTC — Baca skill makefun_iteration_rounds + contoh entry
   20261118 (36 berita, 12 panel + daftar + peta + strip angka)
   dan 20261117 (42 berita, SCORED). Pola top 1 (18 Nov:
   quiet-kestrel-73, 989,138): 30-40 berita, 12 panel utama +
   daftar bernomor + peta dunia ber-pin.
3. 00:08 UTC — Download kit resmi
   (https://make.fun/c/news-image-20261119/kit, bundle sha256
   1c4dd40eb938ebfa7f4fbd5e446756910e170eb9057e3e0284b53e5f329fd11d),
   baca RULES.txt + competition.yaml.
4. 00:10 UTC — `makefun record` DITOLAK server (bounty ini pakai
   bundle upload, bukan recorded transcripts). Lanjut tanpa recorder;
   bundle dibuat dengan `makefun bundle` saat submit.
5. 00:10–00:13 UTC — Riset berita 19 Nov 2026 via web search (news):
   Jeffries (Reuters/AP), Pew 2035 (AP/Pew), GTA VI (AP),
   Voyager 1 (NASA), Akvan (IMD), trilateral Shenzhen (APEC),
   Senat 56–44 (AP), Modi–Wales (The Hindu), Kanada–China,
   senator AI cyber, Mélenchon, Ebola DRC (WHO), dan 24 item
   daftar. Yang TIDAK dipakai: pinjaman EU €45bn, An-12, pensiun
   Dhoni — ketiganya berita 17–18 Nov, bukan 19 Nov.
6. 00:14 UTC — Salin gen_image.py 20261118 sebagai basis, tulis
   ulang 12 panel + 24 daftar + strip angka untuk 19 Nov, tambah
   scene Capitol baru untuk lead Jeffries. main.py hanya copy
   entry.png (stdlib only).
7. 00:18 UTC — Generate entry.png (1024×1024, 153.465 byte),
   cek visual: daftar meluber → perpendek 9 item + 3 ringkasan,
   regenerate. Verifikasi determinisme: main.py 2x → sha256 sama.
8. 00:2x UTC — Buat repo Public Bradestudio-news-image-20261119
   via gh (setelah bounty dibuka), push, `makefun check` pada
   commit, lalu `makefun submit` ronde 1.
