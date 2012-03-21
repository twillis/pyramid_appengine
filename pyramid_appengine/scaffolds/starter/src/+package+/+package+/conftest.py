"""
hooks into py.test to bootstrap app engine
"""
from google.appengine.ext import testbed as aetestbed
from google.appengine.datastore import datastore_stub_util
from google.appengine.tools import dev_appserver_index
import os

__here__ = os.path.abspath(os.path.dirname(__file__))
app_path = os.path.dirname(__here__)


def pytest_runtest_setup(item):
    item.testbed = aetestbed.Testbed()
    item.testbed.activate()
    item.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
    item.policy.SetSeed(2)
    item.testbed.init_datastore_v3_stub()  # consistency_policy=item.policy)
    item.testbed.init_memcache_stub()
    item.testbed.init_taskqueue_stub()
    item.testbed.init_urlfetch_stub()
    item.index_updater = dev_appserver_index.IndexYamlUpdater(app_path)



def pytest_runtest_teardown(item, nextitem):
    if hasattr(item, "index_updater"):
        item.index_updater.UpdateIndexYaml()
    if hasattr(item, "testbed"):
        item.testbed.deactivate()

