#include <unitree/robot/client/client.hpp>
#include <nlohmann/json.hpp>


class TestClient : public unitree::robot::Client 
{
public:
    TestClient()
    : unitree::robot::Client("test")
    {

    }

    void Init()
    {
        SetApiVersion("0.0.0");
        UT_ROBOT_CLIENT_REG_API_NO_PROI(1000);
    }

    int test_api(const std::string parameter = "")
    {
        std::string data;
        int32_t ret = this->Call(1000, parameter, data);
        std::cout << "Call ret: " << ret << std::endl;
        std::cout << data << std::endl;
        return ret;
    }
};


int main(int argc, char** argv)
{
    unitree::robot::ChannelFactory::Instance()->Init(0);


    TestClient client;
    client.Init();
    client.SetTimeout(1.f);

    int count = 0;
    while (true)
    {
        count++;
        client.test_api(std::to_string(count));
        sleep(1);
    }
    

    return 0;
}