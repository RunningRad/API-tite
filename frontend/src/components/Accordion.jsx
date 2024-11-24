import * as React from 'react';
import { styled } from '@mui/material/styles';
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import MuiAccordion from '@mui/material/Accordion';
import MuiAccordionSummary from '@mui/material/AccordionSummary';
import MuiAccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

const Accordion = styled((props) => (
  <MuiAccordion disableGutters elevation={0} square {...props} />
))(({ theme }) => ({
  border: `1px solid ${theme.palette.divider}`,
  '&:not(:last-child)': {
    borderBottom: 0,
  },
  '&::before': {
    display: 'none',
  },
}));

const AccordionSummary = styled((props) => (
  <MuiAccordionSummary
    expandIcon={<ArrowForwardIosSharpIcon sx={{ fontSize: '0.9rem' }} />}
    {...props}
  />
))(({ theme }) => ({
  backgroundColor: 'rgba(0, 0, 0, .03)',
  flexDirection: 'row-reverse',
  '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded': {
    transform: 'rotate(90deg)',
  },
  '& .MuiAccordionSummary-content': {
    marginLeft: theme.spacing(1),
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
}));

const AccordionDetails = styled(MuiAccordionDetails)(({ theme }) => ({
  padding: theme.spacing(2),
  borderTop: '1px solid rgba(0, 0, 0, .125)',
}));

export default function CustomAccordion({ storeData }) {
  const [expanded, setExpanded] = React.useState('panel1');
  const [selectedStore, setSelectedStore] = React.useState(null);
  const [order, setOrder] = React.useState([]);

  const handleChange = (panel) => (event, newExpanded) => {
    setExpanded(newExpanded ? panel : false);
  };

  const handleSelect = (store) => {
    if (selectedStore && selectedStore.name !== store.name) {
      // Clear the cart when changing the store
      setOrder([]);
    }
    setSelectedStore(store);
  };

  const handleAddToOrder = (item) => {
    setOrder((prevOrder) => [...prevOrder, item]);
  };

  return (
    <div>
      {storeData.map((store, index) => (
        <Accordion
          key={index}
          expanded={expanded === `panel${index + 1}`}
          onChange={handleChange(`panel${index + 1}`)}
        >
          <AccordionSummary
            aria-controls={`panel${index + 1}d-content`}
            id={`panel${index + 1}d-header`}
          >
            <Typography>Option {index + 1}: {store.name}</Typography>
            <Button
              variant="outlined"
              size="small"
              onClick={(e) => {
                e.stopPropagation(); // Prevents expanding the accordion
                handleSelect(store);
              }}
            >
              Select
            </Button>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>Menu items:</Typography>
            {store.items && store.items.map((item, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '8px',
                }}
              >
                <Typography>{item.name} -- {item.price}</Typography>
                <Button
                  variant="contained"
                  size="small"
                  onClick={() => {
                    if (selectedStore && selectedStore.name === store.name) {
                      handleAddToOrder(item);
                    } else {
                      alert("You can only add items from the selected store.");
                    }
                  }}
                >
                  Add
                </Button>
              </div>
            ))}
          </AccordionDetails>
        </Accordion>
      ))}
      {selectedStore && (
        <div style={{ marginTop: '20px' }}>
          <Typography variant="h6">Selected Store: {selectedStore.name}</Typography>
        </div>
      )}
      {order.length > 0 && (
        <Card style={{ marginTop: '20px', padding: '16px', backgroundColor: '#f9f9f9' }}>
          <CardContent>
            <Typography variant="h6" style={{ marginBottom: '16px' }}>
              Current Order:
            </Typography>
            <List>
              {order.map((item, idx) => (
                <ListItem key={idx} style={{ paddingLeft: 0 }}>
                  <ListItemText primary={item} />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
