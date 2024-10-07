import { List, ListItem, Card, Progress } from "@/components/mt-wrapper/mt-wrapper";


export default function Home() {
  return (
    <div className="flex w-full flex-col gap-4">
      <h1>Hello World!</h1>
      <Card className="w-96">
      <List>
        <ListItem>Inbox</ListItem>
        <ListItem>Trash</ListItem>
        <ListItem>Settings</ListItem>
      </List>
    </Card>
    <Progress value={50} color="blue"/>
    </div>
  );
}
