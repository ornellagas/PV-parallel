# Paralelní objednávkový systém pro kurýry

Tento projekt simuluje systém restaurace s paralelními vlákny pro příjem objednávek, přípravu jídla, přiřazování kurýrů a doručení. Ukazuje praktické použití souběžného programování a synchronizace sdílených zdrojů.

---

## Funkce

Projekt obsahuje tyto hlavní funkce:

- **Order Receiver** – přijímá nové objednávky a ukládá je do fronty.
- **Kitchen Workers** – paralelně připravují objednávky z fronty.
- **Assignment Engine** – přiřazuje volné kurýry k připraveným objednávkám a simuluje doručení.
- **Monitor** – zobrazuje aktuální stav všech objednávek a ukončí se, jakmile jsou všechny doručeny.

---

## Struktura projektu

Projekt je rozdělen modulárně:

- **core/shared.py** – sdílené proměnné, fronty, mapy objednávek a kurýrů, locky pro synchronizaci.
- **models/order.py** – definice třídy `Order`.
- **engine/order_receiver.py** – generování a příjem objednávek.
- **engine/kitchen_worker.py** – vlákna kuchařů pro přípravu objednávek.
- **engine/assignment.py** – přiřazování kurýrů a simulace doručení.
- **engine/monitor.py** – vlákno monitoru pro sledování stavu systému.
- **main.py** – hlavní spouštěcí soubor.

---

## Konfigurace

Nastavení systému je možné v několika místech:

- **core/shared.py**:
  - `MAX_ORDERS` – maximální počet objednávek, po kterém se systém ukončí.
  - `stop` – globální flag pro ukončení vláken.

- **main.py**:
  - `NUM_KITCHEN_WORKERS` – počet paralelních kuchařů.
  - `NUM_COURIERS` – počet paralelních kurýrů.

---

## Spuštění

1. Ujistěte se, že máte nainstalovaný Python 3.7 nebo vyšší.
2. Otevřete terminál ve složce projektu.
3. Spusťte hlavní soubor příkazem:

```bash
python src/main.py
