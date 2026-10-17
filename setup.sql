-- Run in a dedicated development database/schema using your own role.
-- Choose a region/model supported by your account and grant only the required privileges.
CREATE STAGE IF NOT EXISTS DEMO_IMAGES
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  DIRECTORY = (ENABLE = TRUE);
-- Uploaded images remain on the stage. Define your own retention/cleanup policy.
