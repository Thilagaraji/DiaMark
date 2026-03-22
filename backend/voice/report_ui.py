import tkinter as tk
from .voice_reader import speak, set_voice, stop_voice

def open_voice_panel(data):

    root = tk.Tk()
    root.title("DiaMark Voice Assist")
    root.geometry("350x260")

    voice_state = tk.BooleanVar(value=True)

    def toggle_voice():
        set_voice(voice_state.get())

    def read_report():

        text = f"""
        Patient name {data['name']}.
        Age {data['age']}.
        Body mass index is {data['bmi']}.
        Fingerprint pattern detected is {data['pattern']}.
        Diabetes risk level is {data['risk_level']}.
        Probability score is {round(data['probability'],2)}.
        Please check the generated report for detailed medical explanation.
        """

        speak(text)

    tk.Label(root, text="DiaMark Voice Assist", font=("Arial", 14)).pack(pady=15)

    tk.Checkbutton(
        root,
        text="Enable Voice",
        variable=voice_state,
        command=toggle_voice
    ).pack()

    tk.Button(
        root,
        text="Read Report",
        bg="green",
        fg="white",
        command=read_report
    ).pack(pady=10)

    tk.Button(
        root,
        text="Stop Voice",
        bg="red",
        fg="white",
        command=stop_voice
    ).pack()

    root.mainloop()