# -*- coding: utf-8 -*-

from openerp import models, fields, api

CORE_CATEGORY_TYPE = [('customer',u'客户'),
                      ('supplier',u'供应商'),
                      ('goods',u'商品'),
                      ('payment',u'支出'),
                      ('receipt',u'收入'),
                      ('attribute',u'属性'),
                      ('goods',u'产品')]
CORE_COST_METHOD = [('average',u'移动平均法'),
                    ('fifo',u'先进先出法'),
                    ]

class core_value(models.Model):
    _name = 'core.value'
    name = fields.Char(u'名称')
    type = fields.Char(u'类型', default=lambda self: self._context.get('type'))

class core_category(models.Model):
    _name = 'core.category'
    name = fields.Char(u'名称')
    type = fields.Selection(CORE_CATEGORY_TYPE,u'类型',default=lambda self: self._context.get('type'))

class res_company(models.Model):
    _inherit = 'res.company'
    start_date = fields.Date(u'启用日期')
    quantity_digits = fields.Integer(u'数量小数位')
    amount_digits = fields.Integer(u'单价小数位')
    cost_method = fields.Selection(CORE_COST_METHOD,u'存货计价方法')
    negtive_quantity = fields.Boolean(u'是否检查负库存')

class uom(models.Model):
    _name = 'uom'
    name = fields.Char(u'名称')

class settle_mode(models.Model):
    _name = 'settle.mode'
    name = fields.Char(u'名称')

class partner(models.Model):
    _name = 'partner'
    code = fields.Char(u'编号')
    name = fields.Char(u'名称')
    c_category_id = fields.Many2one('core.category',u'客户类别',
                                       domain=[('type','=','customer')],context={'type':'customer'})
    s_category_id = fields.Many2one('core.category',u'供应商类别',
                                       domain=[('type','=','supplier')],context={'type':'supplier'})
    receivable = fields.Float(u'应收余额')
    payable = fields.Float(u'应付余额')

class goods(models.Model):
    _name = 'goods'
    code = fields.Char(u'编号')
    name = fields.Char(u'名称')
    category_id = fields.Many2one('core.category',u'产品类别',
                                       domain=[('type','=','goods')],context={'type':'goods'})
    uom_id = fields.Many2one('uom',u'计量单位')
    uos_id = fields.Many2one('uom',u'辅助单位')
    conversion = fields.Float(u'转化率(1辅助单位等于多少计量单位)')
    cost = fields.Float(u'成本')
    price_ids = fields.One2many('goods.price','goods_id',u'价格清单')

class goods_price(models.Model):
    _name = 'goods.price'
    goods_id = fields.Many2one('goods','商品')
    category_id = fields.Many2one('core.category',u'客户类别',
                                       domain=[('type','=','customer')],context={'type':'customer'})
    price = fields.Float(u'价格')

class warehouse(models.Model):
    _name = 'warehouse'
    name = fields.Char(u'名称')

class staff(models.Model):
    _name = 'staff'
    name = fields.Char(u'名称')

class bank_account(models.Model):
    _name = 'bank.account'
    name = fields.Char(u'名称')
    balance = fields.Float(u'余额')
