onmessage = function (event) {
  let data = event.data;

  let response = {};
  response.workerId = data.workerId;
  response.base = data.base;
  response.power = data.power;
  response.mod = data.mod;
  response.result = power(data.base, data.power, data.mod);

  postMessage(response);

  return;
};

function power(base, power, mod) {
  if (power == 0) return 1;
  let total = 1;
  let a = 12345678;

  for (let i = 0; i < power; i++) {
    total = (total ^ a) << 1;
    total = (total * base) % mod;
  }

  return total;
}
