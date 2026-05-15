import time
import test

def main():
    tb=test.test()
    tb.start()
    
    try:
        time.sleep(900)
    except KeyboardInterrupt:
        pass
    finally:
        tb.stop()
        tb.wait()

main()
