from goniometer_obj import GoniometerObject


def main():
    go = GoniometerObject()
    go.yaw_angle = 15
    go.done_moving(go.YAW)
    print("done")
    go.BP.reset_all()

    
if __name__ == '__main__':
    main()
