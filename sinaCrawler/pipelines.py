# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi


class SinacrawlerPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        # guid = self._get_guid(item)
        # now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                   INSERT INTO sina_comment (report_url,report_title,report_time,report_content)
                   VALUES (%s,%s,%s,%s)
               """, (item['report_url'], item['report_title'], item['report_time'], item['report_content']))
        spider.log("Item stored in db: %s " % item['report_title'])

        # conn.execute("""SELECT EXISTS(
        #        SELECT 1 FROM hupu WHERE guid = %s
        #    )""", (guid,))
        # ret = conn.fetchone()[0]
        #
        # if ret:
        #     conn.execute("""
        #            UPDATE hupu
        #            SET url=%s
        #            WHERE guid=%s
        #        """, (item['url'], guid))
        #     spider.log("Item updated in db: %s %r" % (guid, item))
        # else:
        #     conn.execute("""
        #            INSERT INTO hupu (guid,url)
        #            VALUES (%s,%s)
        #        """, (guid, item['url']))
        #     spider.log("Item stored in db: %s %r" % (guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)
