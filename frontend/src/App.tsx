import ListGroup from "./components/ListGroup";
import Alert from "./components/Alert";
import TextField from "./components/TextField";

function App() {
  let items = ["option1", "option2", "option3"];
  const handleSelectItem = (item: string) => {
    console.log(item);
  };
  return (
    <div>
      <TextField name="julia" label="input" />
      <ListGroup
        items={items}
        heading="Restaurant Options"
        onSelectItem={handleSelectItem}
      />
      <Alert> Hello World </Alert>
    </div>
  );
}
export default App;
