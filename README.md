# DrogaPL

Wtyczka QGIS 3 do geometrycznego projektowania dróg zgodnie z polskimi
normami technicznymi. Inspirowana projektem
[GeoRoad](https://github.com/matheusfillipe/Topografia) (Brazylia),
ale napisana od zera pod kątem polskich warunków technicznych.

## Status: etap 0 (szkielet)

Ta wersja zawiera:

- rejestrację wtyczki w QGIS (ikona w pasku narzędzi + wpis w menu Plugins),
- panel boczny (dockwidget) z wyborem klasy technicznej drogi (A, S, GP, G, Z, L, D),
- moduł `core/standards.py` z parametrami normowymi dla każdej klasy
  (promienie łuków, prędkości projektowe, maks. pochylenia itd.),
- test jednostkowy `test/test_standards.py`, uruchamialny bez QGIS.

Funkcje docelowe (rysowanie osi trasy, łuki poziome/pionowe, przekroje
poprzeczne, kubatury robót ziemnych, eksport) są widoczne w panelu jako
wyszarzone przyciski — będą aktywowane w kolejnych etapach.

## Instalacja (tryb deweloperski)

1. Spakuj folder `DrogaPL/` do pliku `DrogaPL.zip` (upewnij się, że folder
   `DrogaPL` jest na najwyższym poziomie archiwum, a nie jego zawartość
   bezpośrednio).
2. W QGIS: `Wtyczki -> Zarządzaj i instaluj wtyczki -> Zainstaluj z ZIP`,
   wskaż plik `DrogaPL.zip`.
3. Włącz wtyczkę na liście (jeśli nie włączy się automatycznie).
4. Powinna pojawić się ikona DrogaPL w pasku narzędzi oraz wpis w menu
   `Wtyczki -> DrogaPL`.

### Alternatywa: link symboliczny (szybsze iterowanie podczas developmentu)

Zamiast pakować ZIP przy każdej zmianie, można podlinkować folder
bezpośrednio do katalogu wtyczek QGIS:

```bash
# Linux
ln -s /sciezka/do/DrogaPL ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DrogaPL

# potem w QGIS zainstaluj i włącz wtyczkę "Plugin Reloader"
# (Wtyczki -> Zarządzaj i instaluj wtyczki), żeby przeładowywać kod
# jednym kliknięciem zamiast restartować QGIS za każdym razem.
```

## Testy (bez QGIS)

Logika w `core/` nie zależy od PyQt/PyQGIS, więc można ją testować zwykłym
pytest:

```bash
pip install pytest
pytest test/
```

## Tłumaczenia (i18n)

Kod źródłowy (nazwy zmiennych, funkcji, komentarze) jest po angielsku.
Wszystkie teksty widoczne w interfejsie są owinięte w `self.tr(...)` /
`QCoreApplication.translate(...)`, co pozwala je przetłumaczyć bez
dotykania logiki. Zobacz `i18n/README.md`.

## Struktura projektu

```
DrogaPL/
├── metadata.txt          # metadane wtyczki (wymagane przez QGIS)
├── __init__.py            # classFactory() - punkt wejścia
├── drogapl.py             # główna klasa wtyczki (GUI registration)
├── icon.png
├── core/                  # logika obliczeniowa, bez zależności od GUI
│   └── standards.py       # tabele parametrów wg polskich norm
├── gui/                   # okna dialogowe / dockwidgety
│   └── main_dockwidget.py
├── i18n/                  # tłumaczenia
└── test/                  # testy jednostkowe core/ (pytest, bez QGIS)
```

## Kolejne etapy

1. Rysowanie osi trasy na mapie + obliczanie pikietażu.
2. Łuki poziome: obliczenie promienia z geometrii + walidacja wobec normy,
   wstawianie klotoid.
3. Edytor niwelety (profil podłużny).
4. Łuki pionowe (parabole) + walidacja promieni.
5. Przekroje poprzeczne z rastra DEM + sekcja typowa.
6. Kubatury robót ziemnych (wykop/nasyp) + diagram Brücknera.
7. Eksport: CSV / DXF / GeoPackage, raport PDF.

## Licencja

TODO: wybierz licencję (np. GPL-3.0, zgodnie z konwencją większości
wtyczek QGIS w oficjalnym repozytorium).
