function transform(line) {
  var values = line.split(";");

  var obj = new Object();
  obj.adresse = values[0];
  obj.humidite = values[1];
  obj.niveau_sonore = values[2];
  obj.pollution_air = values[3];
  obj.temperature = values[4];
  obj.timestamp = values[5];
  var jsonString = JSON.stringify(obj);
  return jsonString;
}
