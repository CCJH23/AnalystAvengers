# from db import db

# class ItemService():
#     def get_all_items():
#         try:
#             items = db.get_collection('testcollection').find()

#             itemsOutputList = []
#             for item in items:
#                 name = item['name']
#                 price = item['price']
#                 description = item['description']

#                 itemObj = {
#                     'name': name,
#                     'price': price,
#                     'description': description
#                 }
#                 itemsOutputList.append(itemObj)

#             return itemsOutputList
#         except Exception as e:
#             raise Exception("No items found")
        
