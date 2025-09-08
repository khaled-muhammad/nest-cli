from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button

class MyApp(App):
    CSS_PATH = "styles.css"  # optional CSS file

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("👋 Hello from Textual!", id="hello")
        yield Button("Click me", id="click")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one("#hello", Static).update("✅ Button clicked!")

if __name__ == "__main__":
    app = MyApp()
    app.run()
