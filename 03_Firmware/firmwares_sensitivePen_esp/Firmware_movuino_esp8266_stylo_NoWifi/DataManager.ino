void printMovuinoData() 
{
  /*
   * Print 9 axes data from the movuino
   */
  Serial.print(currentTime);
  Serial.print("\t ");
  Serial.print(-ax);
  Serial.print("\t ");
  Serial.print(ay);
  Serial.print("\t ");
  Serial.print(az);
  Serial.print("\t ");
  Serial.print(gx);
  Serial.print("\t ");
  Serial.print(-gy);
  Serial.print("\t ");
  Serial.print(-gz);
  Serial.print("\t ");
  Serial.print(mx);
  Serial.print("\t ");
  Serial.print(-my);
  Serial.print("\t ");
  Serial.print(-mz);
  Serial.print("\t ");
  Serial.print(pressure);
  Serial.println();
}
void writeInFileMovuinoData(File file, String sep) {
  /*
   * Write in the File "file" all 9 axes data from the movuino separate by the String sep
   */
  file.print(currentTime);
  file.print(sep);
  file.print(-ax);
  file.print(sep);
  file.print(ay);
  file.print(sep);
  file.print(az);
  file.print(sep);
  file.print(gx);
  file.print(sep);
  file.print(-gy);
  file.print(sep);
  file.print(-gz);
  file.print(sep);
  file.print(mx);
  file.print(sep);
  file.print(-my);
  file.print(sep);
  file.print(-mz);
  file.print(sep);
  file.print(pressure);
  file.println();
}
void initialiseFileMovuinoData(File file, String sep) {
  /*
   * Write the name of each column of 9 axes movuino data in the File file
   */
  file.print("time");
  file.print(sep);
  file.print("ax");
  file.print(sep);
  file.print("ay");
  file.print(sep);
  file.print("az");
  file.print(sep);
  file.print("gx");
  file.print(sep);
  file.print("gy");
  file.print(sep);
  file.print("gz");
  file.print(sep);
  file.print("mx");
  file.print(sep);
  file.print("my");
  file.print(sep);
  file.print("mz");
  file.print(sep);
  file.print("pressure");
  file.println();
}

void magnetometerAutoCallibration() {
  int magVal[] = {mx, my, mz};
  for (int i = 0; i < 3; i++) {
    // Compute magnetometer range
    if (magVal[i] < magRange[2 * i]) {
      magRange[2 * i] = magVal[i]; // update minimum values on each axis
    }
    if (magVal[i] > magRange[2 * i + 1]) {
      magRange[2 * i + 1] = magVal[i]; // update maximum values on each axis
    }

    // Scale magnetometer values
    if (magRange[2 * i] != magRange[2 * i + 1]) {
      magVal[i] = map(magVal[i], magRange[2 * i], magRange[2 * i + 1], -100, 100);
    }
  }

  // Update magnetometer values
  mx = magVal[0];
  my = magVal[1];
  mz = magVal[2];
}
