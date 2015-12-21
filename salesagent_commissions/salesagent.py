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


class salesagent_common(osv.osv):

    _name = "salesagent.common"
    _description = "Generic Utilities"

    # ----- Return the right commission percentuage
    def recognized_commission(self, cr, uid, customer_id, salesagent_id,
                              product_id, context=None):
        # ------ Commissions will be searched in this order:
        #       - commission for product for customer
        #       - commission for product for salesagent
        #       - commission for category for customer
        #       - commission for category for salesagent
        #       - commission for product
        #       - commission for customer
        #       - commission for salesagent
        # ----- If the salesagent field in the order is empty, exit
        commission = 0.0
        if not customer_id or not salesagent_id or not product_id:
            return commission
        partner_product_commission_obj = self.pool.get(
            'partner.product_commission')
        partner_category_commission_obj = self.pool.get(
            'partner.category_commission')
        # ----- If customer has a special commission for the product
        lst_commission_product_customer = partner_product_commission_obj.search(
            cr, uid,
            [('name', '=', product_id), ('partner_id', '=', customer_id)])
        if lst_commission_product_customer:
            commission = partner_product_commission_obj.browse(
                cr, uid, lst_commission_product_customer[0]).commission
            return commission
        # ----- If salesagent has a special commission for the product
        lst_commission_product_customer = partner_product_commission_obj.search(
            cr, uid,
            [('name', '=', product_id), ('partner_id', '=', salesagent_id)])
        if lst_commission_product_customer:
            commission = partner_product_commission_obj.browse(
                cr, uid, lst_commission_product_customer[0]).commission
            return commission
        # ----- If salesagent has a special commission for the category
        category_id = self.pool.get('product.product').browse(
            cr, uid, product_id).categ_id.id
        lst_commission_category_agent = partner_category_commission_obj.search(
            cr, uid,
            [('name', '=', category_id), ('partner_id', '=', salesagent_id)])
        if lst_commission_category_agent:
            commission = partner_category_commission_obj.browse(
                cr, uid, lst_commission_category_agent[0]).commission
            return commission
        # ----- If customer has a special commission for the category
        category_id = self.pool.get('product.product').browse(
            cr, uid, product_id).categ_id.id
        lst_commission_category_customer = partner_category_commission_obj.search(
            cr, uid,
            [('name', '=', category_id), ('partner_id', '=', customer_id)])
        if lst_commission_category_customer:
            commission = partner_category_commission_obj.browse(
                cr, uid, lst_commission_category_customer[0]).commission
            return commission
        # ----- If product has a special generic commission
        commission = self.pool.get('product.product').browse(
            cr, uid, product_id).commission
        if commission:
            return commission
        # ----- If customer has a special generic commission
        commission = self.pool.get('res.partner').browse(cr, uid,
                                                         customer_id).commission
        if commission > 0.0:
            return commission
        # ----- If salesagent has a special generic commission
        commission = self.pool.get('res.partner').browse(
            cr, uid, salesagent_id).commission
        return commission

    # ----- Calcola la provvigione totale da riconoscere all'agente
    def commission_calculate(self, cr, uid, param_class, id, context=None):
        '''
        @classe : Indica la classe di riferimento per gli id passati al parametro ids
        @id : id della classe di cui si vuole calcolare la provvigione
        '''
        class_brows = self.pool.get(param_class).browse(cr, uid, id, context)
        total_commission = 0.0
        if param_class == 'account.invoice.line':
            salesagent_id = (
                class_brows.invoice_id and
                class_brows.invoice_id.salesagent_id and
                class_brows.invoice_id.salesagent_id.id or
                context.get('salesagent_id', False))
            customer_id = (
                class_brows.invoice_id and
                class_brows.invoice_id.partner_id and
                class_brows.invoice_id.partner_id.id or
                context.get('partner_id', False))
            product = class_brows.product_id or False
            total_price = class_brows.price_subtotal
        percentage_commission = self.recognized_commission(
            cr, uid, customer_id, salesagent_id,
            product and product.id or False,
            context=context)
        if percentage_commission:
            total_commission = (total_price * percentage_commission) / 100
        return total_commission

salesagent_common()
