# Visual Quality Assistant

A Streamlit reference app for image observations using Snowflake Cortex. Upload images, ask a
question, edit the generated observations and export a Word report with the images attached.
The public edition retains the Snowpark/key-pair integration and category utilities while replacing
the original organisation-specific taxonomy and report template.

## Architecture

Image upload → unique temporary filename → Snowflake stage → parameterised `AI_COMPLETE` call →
editable observations → DOCX generated in memory. Temporary local files are removed automatically.

## Setup

Requires Python 3.11+, a Snowflake warehouse, a Cortex-enabled role and a supported image model.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Configure your account, private key path and MODEL_NAME.
# Run setup.sql in your dedicated Snowflake development database/schema.
streamlit run app.py
```

`STAGE_NAME` defaults in the example to `DEMO_IMAGES`; fully qualify it if needed. Grant the role
only the permissions needed for the selected stage and Cortex model. Keep key files outside Git.
Uploaded images remain in your Snowflake stage; configure a retention/cleanup process there.
Use synthetic or authorised images. The model may misinterpret images or text embedded in them.

## Included examples

`codes/defect_codes.json` contains three invented `DEMO-*` categories. They are demonstration
labels, not a regulatory codebook. Observations require human review and are not safety certification.
The public UI creates its own generic DOCX report and has no dependency on a private report binary.

## Validation

```bash
python -m unittest discover -s tests -v
```

3 offline tests pass for SQL parameter binding, category schema and prompt boundaries. Python
source compiles. Live Snowflake inference and account-specific stage permissions remain untested.

API reference: [Snowpark SQL parameters](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.Session.sql)
and [TO_FILE](https://docs.snowflake.com/en/sql-reference/functions/to_file).

## Public edition

This is a separately prepared portfolio edition with fresh history. Private deployment settings,
credentials, operational records, uploads, backups and organisation-specific assets are excluded.
See [PUBLIC_EDITION.md](PUBLIC_EDITION.md). No deployment workflows are included.
