from google_transfer1_0.core.service.api.basicTestAPI.tests.main import ClassTester as stdAPI
from google_transfer1_0.core.service.api.client_apis.transfer_info.specific.tests.main import ClassTester as specificTransferAPI
from google_transfer1_0.core.service.api.client_apis.transfer_info.base.tests.main import ClassTester as baseTransferAPI
from google_transfer1_0.core.service.api.client_apis.file_api.tests.main import ClassTester as TransferFilesAPI
from google_transfer1_0.core.service.api.APICore import API
from google_transfer1_0.core.service.api.root.BuildAPI import BuildAPI
from google_transfer1_0.core.service.api.root.conf.conf import conf as APIConfiguration

def testAddToFlask(api: [API]):
    app=BuildAPI(
        apiConfig=APIConfiguration,
        apis=api)

    app.build()

testAddToFlask(
    [stdAPI,
     specificTransferAPI,
     baseTransferAPI,
     TransferFilesAPI])
#print("tests complete")