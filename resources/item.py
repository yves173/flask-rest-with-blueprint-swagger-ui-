import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items,stores


blp=Blueprint('items',__name__,description='Opreration on the Items')


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404,'item can not be found!')

    def put(self,item_id):
        itemdata=request.get_json()
        try:
            item=items[item_id]
            item |=itemdata
            return item,201
        except KeyError:
            abort(404,'store can not be found!')

    def delete(self,item_id):
        try:
            del items[item_id]
            return {'message':f'item {item_id} is deleted'}
        except KeyError:
            abort(404,'store can not be found!')



@blp.route('/item')
class ItemList(MethodView):

    def get(self):
        return {'items':list(items.values())}

    def post(self):
        itemdata=request.get_json()
        if itemdata['store_id'] not in stores:
            abort(404,'store can not be found!')

        itemId=uuid.uuid4().hex
        newItem={**itemdata,'item_id':itemId}
        items[itemId]=newItem
        return newItem,201