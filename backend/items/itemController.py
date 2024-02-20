# from flask import jsonify, Blueprint
# from items.itemService import ItemService

# itemBp = Blueprint('item', __name__)

# @itemBp.route('/get_all_items')
# def get_all_items():
#     try:
#         response = ItemService.get_all_items()
#         return jsonify(response), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

