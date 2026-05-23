# Dokumentacja CI/CD

Automatyczny potok GitHub Actions poprawnie buduje aplikację i publikuje ją w rejestrze GHCR.

## Realizacja etapów zadania

1. Multi-Arch: Użycie QEMU i Docker Buildx umożliwiło jednoczesną budowę obrazu na architektury linux/amd64 oraz linux/arm64.
2. Uprawnienia GHCR: Pierwsze błędy autoryzacji (denied) naprawiono dodaniem do pliku YAML uprawnień zapisu pakietów (packages: write).
3. Test CVE: Skaner Trivy sprawdza obraz pod kątem luk HIGH i CRITICAL. Wynik w formie tabeli trafia do logów, a kod wyjścia zero pozwala na publikację obrazu przy pełnej widoczności raportu.
4. Pamięć podręczna (Cache): Dane cache są wysyłane do osobnego repozytorium na Docker Hubie za pomocą mechanizmu registry w trybie mode=max, co skróciło czas budowania o ponad 60 procent.

## Strategia tagowania

* Obraz w GHCR: ghcr.io/makson1402/projekt-pogoda-ci:latest
* Cache w Docker Hub: makson1402/projekt-pogoda-cache:max

Uzasadnienie:
Tag latest dla aplikacji zapewnia automatyczne pobieranie najnowszej, stabilnej wersji bez edycji skryptów wdrożeniowych. Wydzielenie cache z tagiem max do zewnętrznego rejestru zapobiega zaśmiecaniu głównego profilu na GitHubie i pozwala Dockerowi na szybkie wznawianie pracy na gotowych warstwach pośrednich.
