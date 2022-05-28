self.onmessage = function (evt) {
  const { module, memory } = evt.data;
  const instance = new WebAssembly.Instance(module, { env: { mem: memory } });
};
