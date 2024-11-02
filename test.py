from Taskara import Taskara as TK


tk = TK()

tk.ln()
tk.ln("text")
context = {
    'hi': "testing",
    "another": "teeeest"
}
tk.add_task("this is first task", TK.mode.TODO)
tk.add_task("this is 2d task", TK.mode.WARN)
tk.add_task("this is third task", TK.mode.INFO)
tk.add_task(context, TK.mode.DEBUG)
tk.add_task(['test', "test2"], TK.mode.DEBUG)
tk.print()
# tk.print_all()
