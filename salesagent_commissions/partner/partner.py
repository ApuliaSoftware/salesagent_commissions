# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Andrea Cometa All Rights Reserved.
#                       www.andreacometa.it
#                       openerp@andreacometa.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from osv import fields, osv


class res_partner(osv.osv):

    _inherit = "res.partner"

    def fill_products(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        product_ids = product_obj.search(
            cr, uid, [('standard_commission_product', '=', True)])
        if not product_ids:
            return True
        products = product_obj.browse(cr, uid, product_ids)
        for id in ids:
            for product in products:
                self.pool.get('partner.product_commission').create(
                    cr, uid, {'partner_id':id, 'name':product.id})
        return True

    def fill_categories(self, cr, uid, ids, context=None):
        category_obj = self.pool.get('product.category')
        category_ids = category_obj.search(
            cr, uid, [('standard_commission_category', '=', True)])
        if not category_ids:
            return True
        categories = category_obj.browse(cr, uid, category_ids)
        for id in ids:
            for category in categories:
                self.pool.get('partner.category_commission').create(cr, uid,
                    {'partner_id':id, 'name':category.id})
        return True

    _columns = {
        'salesagent': fields.boolean("Salesagent"),
        # ----- Relation with customers
        'customer_for_salesagent_ids': fields.one2many(
            'res.partner', 'salesagent_for_customer_id', 'Customers',
            readonly=True),
        # ----- Relation with salesagent
        'salesagent_for_customer_id': fields.many2one(
            'res.partner', 'Salesagent'),
        # ----- General commission for salesagent
        'commission' : fields.float('Commission %'),
        'product_provvigioni_ids': fields.one2many(
            'partner.product_commission', 'partner_id',
            'Commission for products'),
        'category_provvigioni_ids': fields.one2many(
            'partner.category_commission', 'partner_id',
            'Commission for categories'),
        # ----- Relation with salesagent parent
        'salesagent_parent_id': fields.many2one(
            'res.partner', 'Salesagent parent',
            domain="[('salesagent', '=', True)]"),
        'parent_commission' : fields.float('Parent Commission %'),
        #'salesagent_parent_ids': fields.one2many(
        #    'res.partner', 'salesagent_parent_id',
        #    'Sub salesagents'),
    }

res_partner()


class partner_product_commission(osv.osv):

    _name = "partner.product_commission"
    _description = "Relation for Partner, products and commissions"

    _columns = {
        'name': fields.many2one('product.product', 'Product'),
        'commission': fields.float('Commission'),
        'partner_id': fields.many2one('res.partner', 'Partner'),
        }

partner_product_commission()


class partner_category_commission(osv.osv):

    _name = "partner.category_commission"
    _description = "Relation for Partner, product categories and commissions"

    _columns = {
        'name': fields.many2one('product.category', 'Category'),
        'commission': fields.float('Commission'),
        'partner_id': fields.many2one('res.partner', 'Partner'),
        }

partner_product_commission()
