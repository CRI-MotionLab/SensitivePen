#if !defined(_MOVUINOESP32_PRESSURESENSOR_)
#define _MOVUINOESP32_PRESSURESENSOR_

class MovuinoPressureSensor
{
#define N 100
#define WINDOW 500
private:
    int _sensorPin = 38;  // select the input pin for the potentiometer
    int _ledPin = 13;     // select the pin for the LED
    int _sensorValue = 0; // variable to store the value coming from the sensor

    int dataCollect[N];
    int curIndex = 0;
    float curMean = 0.0f;
    float oldMean = 0.0f;

    int indxWindw = 0;
    float minWindw = 1024;
    float maxWindw = 0;
    float curMinWindow = 0;
    float curMaxWindow = 1024;
    float curMeanWindow = 512;

    long timePrint0 = 0;
    int dlyPrint = 10;

    boolean isPress = false;

public:
    MovuinoPressureSensor(/* args */);
    ~MovuinoPressureSensor();

    void begin();
    void update();
};

MovuinoPressureSensor::MovuinoPressureSensor(/* args */)
{
}

MovuinoPressureSensor::~MovuinoPressureSensor()
{
}

void MovuinoPressureSensor::begin()
{
    pinMode(this->_ledPin, OUTPUT);

    // init data collection
    for (int i = 0; i < N; i++)
    {
        this->dataCollect[i] = 0;
    }
}

void MovuinoPressureSensor::update()
{
    // update index
    if (this->curIndex < N && this->curIndex >= 0)
    {
        this->curIndex++;
    }
    else
    {
        this->curIndex = 0;
    }

    // update data collection
    this->dataCollect[this->curIndex] = analogRead(this->_sensorPin);

    // get moving mean
    this->oldMean = this->curMean;
    this->curMean = 0.0f;
    for (int i = 0; i < N; i++)
    {
        this->curMean += this->dataCollect[i];
    }
    this->curMean /= N;

    // update window
    if (this->indxWindw < WINDOW)
    {
        this->indxWindw++;
        if (this->curMean < this->minWindw)
        {
            this->minWindw = this->curMean;
        }
        if (this->curMean > this->maxWindw)
        {
            this->maxWindw = this->curMean;
        }
    }
    else
    {
        // update new thresholds
        this->curMinWindow = this->minWindw;
        this->curMaxWindow = this->maxWindw;
        this->curMeanWindow = (this->curMinWindow + this->curMaxWindow) / 2.0;

        // reset
        this->indxWindw = 0;
        this->minWindw = 1024;
        this->maxWindw = 0;
    }

    // TEST THRESHOLDS
    if (!this->isPress)
    {
        if (this->oldMean <= this->curMaxWindow && this->curMean >= this->curMaxWindow)
        {
            this->isPress = true;
        }
    }
    else
    {
        if (this->oldMean >= this->curMeanWindow && this->curMean <= this->curMeanWindow)
        {
            this->isPress = false;
        }
    }

    if (millis() - this->timePrint0 > this->dlyPrint)
    {
        // Serial.print(dataCollect[curIndex]);
        // Serial.print('\t');
        Serial.print(this->curMean);
        /* Serial.print('\t');
        Serial.print(curMinWindow);
        Serial.print('\t');
        Serial.print(curMaxWindow);
        Serial.print('\t');
        Serial.print(curMeanWindow);
        Serial.print('\t');*/
        /* if(isPress) {
          Serial.print(3000);
        } else {
          Serial.print(3600);
        }*/
        Serial.println("");
        // analogWrite(ledPin, curMean);
        this->timePrint0 = millis();
    }
}

#endif // _MOVUINOESP32_PRESSURESENSOR_