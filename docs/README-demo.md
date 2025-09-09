# Demo Script (60–90 seconds)

1) **Open dashboard** at http://localhost:5050. Say:
   > "This is a minimal digital twin. The motor on the left streams RPM and temperature. The twin visualizes it live and raises alerts."

2) **Start chart updates** (if paused). Point to **Temperature** & **RPM** updating.

3) **Show control loop**:
   - Click **Stop Motor** → terminal shows "Motor is stopped…" and chart flat-lines.
   - Click **Start Motor** → streaming resumes.

4) **Trigger alert**:
   - In `motor_sim.py`, temporarily change temp range to:
     ```python
     "temperature": round(random.uniform(92, 110), 2)
     ```
   - Save & run simulator → UI shows **⚠️ Overheating!**

5) **Wrap**:
   > "So this demonstrates the core twin loop: physical asset → telemetry → twin insights → control back to the asset. Next steps could be history/CSV, multi-asset, or cloud deploy."

