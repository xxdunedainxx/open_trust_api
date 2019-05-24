from ...basicTestAPI.conf.api.conf import conf as APIConfig
from ..basicAPI import BasicAPI
from ...root.BuildAPI import BuildAPI
from ...root.conf.conf import conf as APIConfiguration

def testClassImplementation():
    Tester=BasicAPI(apiConfig=APIConfig,services=[])
    return Tester

ClassTester=testClassImplementation()

def testAddToFlask(api: BasicAPI):
    app=BuildAPI(
        apiConfig=APIConfiguration,
        apis=[api])

    app.build()


#testAddToFlask(ClassTester)
#print("tests complete")