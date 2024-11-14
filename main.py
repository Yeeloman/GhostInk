from ghostink import GhostInk
# from pathlib import Path

ink = GhostInk(project_root='.')
shade = ink.get_shades()
# nested_dict = {
#     "user": {
#         "id": 101,
#         "username": "testuser",
#         "attributes": {
#             "height": 5.9,
#             "hobbies": ["reading", "coding", "hiking"]
#         }
#     }
# }
# ink.drop(nested_dict, shade.DEBUG, ['database', 'api'])
# ink.drop('this an info ask', shade.INFO, ['test', 'api'])
# ink.drop('this an todo ask', shade.TODO, ['leaks'])
# ink.drop('this an warn ask', shade.WARN, ['database'])
ink.drop(filename="example")
ink.whisper()
# ink.clean()
