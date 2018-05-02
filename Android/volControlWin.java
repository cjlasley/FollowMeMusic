





public float calcNewVolume(float distance) {
    float newVol;
newVol = distance;
    return newVol;
}



public void setVolume(float newVol) {
    FloatControl volume = (FloatControl) line.getControl(FloatControl.Type.MASTER_GAIN);
    volume.setValue(newVol);

}





