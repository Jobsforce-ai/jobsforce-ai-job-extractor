const nodeapp = require("./app");
const port = process.env.PORT || 9000;

nodeapp.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
