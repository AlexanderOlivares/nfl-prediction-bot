import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sentry_sdk

if "PRODUCTION" in os.environ:
    from env_configs import prod_config as config
else:
    from env_configs import dev_config as config

try:
    driver = config.driver

    driver.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
    ###############################################################################
    pre_element = driver.find_element_by_tag_name('pre')
    text = pre_element.text
    print("text vvv")
    print(text)

    try:
        cur = config.cursor
        conn = config.conn

        create_table = (
            f"""
            CREATE TABLE IF NOT EXISTS write_test( 
            version VARCHAR(255)
            )
            """
        )

        cur.execute(create_table)
        conn.commit()

        # insert_command = f'INSERT INTO write_test (version) VALUES (%s)'
        # insert_values = (text,)
        # cur.execute(insert_command, insert_values)

        insert_command = f'UPDATE write_test SET version = (%s) WHERE version = (%s)'
        insert_value = ('jaxx wuz here', text)
        cur.execute(insert_command, insert_value)

        conn.commit()
    except Exception as error:
        print(error)
        sentry_sdk.capture_exception(error)
    finally:
        if cur is not None:
            print('cursor was open')
            cur.close()
        if conn is not None:
            print('connection was successful')
            conn.close()

except TimeoutException:
    print(str(TimeoutException))
    sentry_sdk.capture_exception(TimeoutException)
    driver.quit()

except Exception as error:
    print(str(error))
    sentry_sdk.capture_exception(error)
    driver.quit()

finally:
    driver.quit()
