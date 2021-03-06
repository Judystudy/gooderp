# -*- coding: utf-8 -*-

from openerp import tools
import openerp.addons.decimal_precision as dp
from openerp import models, fields


class report_lot_status(models.Model):
    _name = 'report.lot.status'
    _auto = False

    goods = fields.Char(u'产品')
    uom = fields.Char(u'单位')
    lot = fields.Char(u'序列号')
    status = fields.Char(u'状态')
    warehouse = fields.Char(u'仓库')
    date = fields.Date(u'日期')
    qty = fields.Float(u'数量', digits_compute=dp.get_precision('Goods Quantity'))

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_lot_status')
        cr.execute(
            """
            create or replace view report_lot_status as (
                SELECT MIN(line.id) as id,
                        goods.name as goods,
                        uom.name as uom,
                        line.lot as lot,
                        '在库' as status,
                        wh.name as warehouse,
                        max(line.date) as date,
                        sum(line.qty_remaining) as qty

                FROM wh_move_line line
                    LEFT JOIN goods goods ON line.goods_id = goods.id
                    LEFT JOIN uom uom ON line.uom_id = uom.id
                    LEFT JOIN warehouse wh ON line.warehouse_dest_id = wh.id

                WHERE line.lot IS NOT NULL
                  AND line.qty_remaining > 0
                  AND wh.type = 'stock'

                GROUP BY goods, uom, lot, warehouse

                ORDER BY goods, lot, warehouse
            )
        """)
