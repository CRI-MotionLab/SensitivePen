#if !defined(_MOVUINOESP32_PRESSURESENSOR_)
#define _MOVUINOESP32_PRESSURESENSOR_

#define N 3
#define WINDOW 50
#define PIN_PRESSURE 38

class MovuinoPressureSensor
{
private:
    int _sensorValue = 0; // variable to store the value coming from the sensor

    int _dataCollect[N];
    int _curIndex = 0;
    float _curMean = 0.0f;
    float _oldMean = 0.0f;

    int _indxWindw = 0;
    float _minWindw = 4095;
    float _maxWindw = 0;
    float _curMinWindow = 0;
    float _curMaxWindow = 0;
    float _curMeanWindow = 0;

    long _timer0 = 0;
    int _rateTime = 10; // time between data (ms)

    bool _isPress = false;

public:
    MovuinoPressureSensor(/* args */);
    ~MovuinoPressureSensor();

    void begin();
    void update();
    void printData();
    bool isTouch();
    float getPressure();
};

MovuinoPressureSensor::MovuinoPressureSensor(/* args */)
{
}

MovuinoPressureSensor::~MovuinoPressureSensor()
{
}

void MovuinoPressureSensor::begin()
{
    // init data collection
    for (int i = 0; i < N; i++)
    {
        this->_dataCollect[i] = 0;
    }
}

void MovuinoPressureSensor::update()
{
    if (millis() - this->_timer0 > this->_rateTime)
    {
        this->_timer0 = millis(); // reset

        // update index
        if (this->_curIndex < N && this->_curIndex >= 0)
        {
            this->_curIndex++;
        }
        else
        {
            this->_curIndex = 0;
        }

        // update data collection
        this->_dataCollect[this->_curIndex] = analogRead(PIN_PRESSURE);

        // get moving mean
        this->_oldMean = this->_curMean;
        this->_curMean = 0.0f;
        for (int i = 0; i < N; i++)
        {
            this->_curMean += this->_dataCollect[i];
        }
        this->_curMean /= N;

        // update window
        if (this->_indxWindw < WINDOW)
        {
            this->_indxWindw++;
            if (this->_curMean < this->_minWindw)
            {
                this->_minWindw = this->_curMean;
            }
            if (this->_curMean > this->_maxWindw)
            {
                this->_maxWindw = this->_curMean;
            }
        }
        else
        {
            // update new thresholds
            this->_curMinWindow = this->_minWindw;
            this->_curMaxWindow = this->_maxWindw;
            this->_curMeanWindow = (this->_curMinWindow + this->_curMaxWindow) / 2.0;

            // reset
            this->_indxWindw = 0;
            this->_minWindw = 4095;
            this->_maxWindw = 0;
        }
    }
}

void MovuinoPressureSensor::printData()
{
    Serial.print(this->_curMean);
    Serial.print('\t');
    Serial.print(this->_curMinWindow);
    Serial.print('\t');
    Serial.print(this->_curMaxWindow);
    Serial.print('\t');
    Serial.print(this->_curMeanWindow);
    Serial.print('\t');

    if (this->isTouch())
    {
        Serial.print(this->_curMeanWindow + 0.5 * (this->_curMeanWindow - this->_curMinWindow));
    }
    else
    {
        Serial.print(this->_curMinWindow + 0.5 * (this->_curMeanWindow - this->_curMinWindow));
    }
    Serial.println("");
}

bool MovuinoPressureSensor::isTouch()
{
    if (!this->_isPress)
    {
        if (this->_oldMean <= this->_curMeanWindow && this->_curMean >= this->_curMeanWindow)
        {
            this->_isPress = true;
        }
    }
    else
    {
        if (this->_oldMean >= this->_curMeanWindow && this->_curMean <= this->_curMeanWindow)
        {
            this->_isPress = false;
        }
    }
    return this->_isPress;
}

float MovuinoPressureSensor::getPressure()
{
    float press_ = 0.0f;
    press_ = (this->_curMean - this->_curMeanWindow) / (this->_curMaxWindow - this->_curMinWindow);
    // if (this->isTouch())
    // {
    //     if (this->_curMaxWindow > this->_curMeanWindow)
    //     {
    //         press_ = (this->_curMean - this->_curMeanWindow) / (this->_curMaxWindow - this->_curMeanWindow);
    //     }
    // }
    // return press_;
    return this->_curMean;
}

#endif // _MOVUINOESP32_PRESSURESENSOR_