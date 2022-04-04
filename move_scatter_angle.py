from goniometer_obj import GoniometerObject


def main():
    go = GoniometerObject()
    #print(go.led_angle)
    go.scatter_angle = -5
    go.done_moving(go.SCATTER)
    print("done")
    go.BP.reset_all()

    
if __name__ == '__main__':
    main()