# Tłumaczenia (i18n)

Kod źródłowy jest po angielsku, ale wszystkie teksty widoczne w GUI są
owinięte w `self.tr("...")`, co pozwala je tłumaczyć bez zmiany kodu.

## Jak wygenerować / zaktualizować plik tłumaczenia

Wymaga zainstalowanego Qt Linguist (`pyqt5-dev-tools` na Ubuntu/Debian,
albo pakietu `qt5-tools`).

1. Wygeneruj / zaktualizuj plik `.ts` na podstawie kodu źródłowego:

   ```bash
   pylupdate5 -verbose ../drogapl.py ../gui/main_dockwidget.py -ts DrogaPL_pl.ts
   ```

2. Otwórz `DrogaPL_pl.ts` w Qt Linguist i przetłumacz brakujące stringi
   (choć w tym projekcie teksty w `tr()` są już pisane po polsku, więc
   `DrogaPL_pl.ts` w praktyce będzie tożsamościowy — przyda się głównie
   gdybyś chciał dodać wersję angielską GUI: wtedy `tr()` powinno zawierać
   teksty angielskie, a tłumaczenie polskie/inne idzie przez `.ts`).

3. Skompiluj do binarnego `.qm`, które wczytuje wtyczka w runtime:

   ```bash
   lrelease DrogaPL_pl.ts
   ```

4. Upewnij się, że plik `DrogaPL_pl.qm` znajduje się w `i18n/` — plugin
   ładuje go automatycznie na podstawie ustawień języka w QGIS
   (`locale/userLocale` w `QSettings`).

## Uwaga dot. konwencji w tym projekcie

Aktualnie stringi w `tr()` są pisane od razu po polsku (bo to język
docelowych użytkowników wtyczki), a nie po angielsku jak zwykle bywa w
międzynarodowych projektach Qt. To świadoma decyzja — jeśli w przyszłości
zechcesz udostępnić wtyczkę też w innych językach, warto rozważyć zmianę
tekstów źródłowych w `tr()` na angielskie i dodanie `DrogaPL_pl.ts` jako
tłumaczenia "z powrotem" na polski, żeby zachować standardową konwencję.
