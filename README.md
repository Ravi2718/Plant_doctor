# 🌱 Plant Doctor

A friendly AI-powered desktop app that helps you check the health of your plant and gives warm, emoji-filled care tips.  
Uses **Tkinter** for the GUI and can optionally use **OpenAI GPT** for smarter advice.

---

## ✨ Features
- Simple form to enter plant details.
- Basic offline analysis when GPT is not available.
- GPT-powered plant care tips (requires OpenAI API key).
- Colorful, emoji-rich feedback.
- Detects possible issues with soil, pests, and watering.

---

## 📦 Requirements
Python 3.8+ recommended.

Install dependencies:
```bash
pip install pillow openai
````

---

## 🔑 API Key Setup (Optional for GPT mode)

If you want AI-powered analysis, you’ll need an OpenAI API key.

1. Get your API key from [OpenAI](https://platform.openai.com/).
2. Open `main.py` and replace:

   ```python
   api_key = "YOUR_API_KEY_HERE"
   ```

   with your actual key.

If you skip this step, the app will still run using the basic offline analysis.

---

## 📂 Project Structure

```
plant_doctor/
│
├── main.py      # Backend logic for analysis
├── ui.py        # Tkinter-based GUI
├── image/
│   └── logo.png # Logo image for the UI
└── README.md
```

---
## 📽️ Project Demo
<p align="center">
  <a href="https://youtu.be/dInbPsSmhc4">
    <img src="https://img.youtube.com/vi/dInbPsSmhc4/0.jpg?v=2" alt="Watch the Plant Doctor Demo" width="600">
  </a>
</p>

## ▶️ How to Run

1. Make sure you have all dependencies installed.
2. Check that `logo.png` exists in the `image` folder and update `ui.py`’s `logo_path` if needed.
3. Start the app:

   ```bash
   python ui.py
   ```

---

## 🖥️ How to Use

1. Launch the app.
2. Fill in:

   * Flower Name 🌸
   * Plant Color 🎨
   * Age of the Plant 🌱
   * Soil Type 🌍
   * Mature Level 📈
   * Patches? 🪲
3. Click **Submit**.
4. View your plant’s status and tips in a nicely formatted box.
5. Click **Back to Lobby** to check another plant.

---

## 📝 Notes

* If your `python` command runs a different Python version, adjust the `subprocess` call in `ui.py` to `python3` or your correct interpreter path.
* For best results, run on Windows or macOS with UTF-8 encoding enabled.

