# Paralelní logistický a objednávkový systém

Tento projekt simuluje pokročilý systém restaurace s paralelními vlákny pro příjem objednávek přes API, přípravu jídla, automatické přiřazování kurýrů a real-time monitoring přes WebSockety. Ukazuje kombinaci vícevláknového (Multi-threading) a asynchronního programování.

---

## Funkce

Projekt obsahuje tyto hlavní funkce:

- **FastAPI Receiver** – přijímá objednávky přes HTTP POST a okamžitě je zařazuje do systému.
- **Kitchen Workers** – paralelní vlákna kuchařů, která zpracovávají objednávky z fronty a simulují přípravu.
- **Assignment Engine** – automatický dispečer, který páruje hotová jídla s volnými kurýry a zajišťuje doručení.
- **Real-time Dashboard** – webové rozhraní, které pomocí WebSocketů živě zobrazuje každou změnu stavu bez nutnosti obnovy stránky.

---

## Struktura projektu

Projekt je rozdělen modulárně:

- **core/shared.py** – komunikační jádro: fronty, zámky (locks) a WebSocket manager pro rozesílání zpráv.
- **models/order.py** & **models/courier.py** – definice datových tříd pro objednávky a kurýry.
- **engine/api.py** – definice API endpointů a interaktivního HTML dashboardu.
- **engine/kitchen_worker.py** – logika kuchařů pracujících v paralelních vláknech.
- **engine/assignment.py** – logika dispečinku a správa doručování.
- **engine/init_couriers.py** – inicializace počátečního počtu kurýrů.
- **main.py** – hlavní spouštěcí soubor, který koordinuje start všech vláken a serveru.

---

## Konfigurace

Nastavení systému je možné v těchto místech:

- **main.py**:
  - `init_couriers(5)` – počet kurýrů v systému.
  - `range(1, 4)` – počet paralelně běžících kuchařů.

- **engine/kitchen_worker.py**:
  - `random.uniform(3, 6)` – délka přípravy jídla (v sekundách).

---

## Spuštění

1. Ujistěte se, že máte nainstalovaný Python 3.10+ a knihovny `fastapi` a `uvicorn`. (pip install fastapi uvicorn)
2. Otevřete terminál ve složce projektu.
3. Spusťte hlavní soubor příkazem:

```bash
python src/main.py
