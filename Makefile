OUT_FILE?=./school_run.zip
DELIVERABLE=$(abspath $(OUT_FILE))

install:
	pipenv install --three

clean:
	pipenv clean
	rm -f ${DELIVERABLE}

package:
	$(eval VENV = $(shell pipenv --venv))
	cd ${VENV}/lib/python3.7/site-packages && zip -r9 ${DELIVERABLE} ./*
	zip -r9 ${DELIVERABLE} school_run

deploy:
	aws s3 cp ${DELIVERABLE} s3://school-run-artifacts/deploy.zip
	aws lambda update-function-code \
      --function-name school-run-lambda \
      --s3-bucket school-run-artifacts \
      --s3-key deploy.zip --region eu-west-1