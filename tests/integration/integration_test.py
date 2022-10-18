import asyncio
import pytest


@pytest.mark.asyncio
async def test_application(ops_test):
    my_charm = await ops_test.build_charm(".")
    application_name = "discourse"
    await ops_test.model.deploy("postgresql-k8s")
    await ops_test.model.deploy("redis-k8s")
    await ops_test.model.wait_for_idle()

    await ops_test.model.deploy(
        my_charm,
        series="focal",
        application_name=application_name,
        config={
            'external_hostname': 'test.test',
            'discourse_image': "localhost:32000/discourse:test",
            'developer_emails': 'admin@email.test',
            'smtp_domain': 'email.test',
            'smtp_address': '172.31.79.34',
            'smtp_port': '25',
            's3_enabled': True,
            's3_endpoint': 'http://172.31.78.233:8080',
            's3_bucket': 'discourse',
            's3_access_key_id': '1c7565ac7fb74d448e561459ee3f8aa1',
            's3_secret_access_key': '4bf64708933e40e3b5dd81e1981d1043',
            's3_backup_bucket': 'discourse-backup',
            's3_region': 'us-east-1'
        }
    ),
    await ops_test.model.wait_for_idle()

    application = ops_test.model.applications[application_name]
    await ops_test.model.add_relation(application_name, "postgresql-k8s:db-admin")
    await ops_test.model.add_relation(application_name, "redis-k8s")

    await ops_test.model.wait_for_idle()
    return application
