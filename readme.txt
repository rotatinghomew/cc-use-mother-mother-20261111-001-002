医疗指南网页证据快照网
医院知识运营人员用离线回放响应采集公开指南页面，去除模板噪声、建立版本差异和证据链，供医生审核参考。

测试：python3 -m unittest discover -s tests/guideline_mirror -p 'test_*.py'
构建：python3 -m compileall -q evidence_mesh tests/guideline_mirror
验收：python3 -m evidence_mesh.operator.snapshot_cli --fixture fixtures/demo.json --database /tmp/guideline_mirror-acceptance.sqlite3
