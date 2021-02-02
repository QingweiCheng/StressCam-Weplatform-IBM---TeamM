import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Typography from '@material-ui/core/Typography';
import InputLabel from '@material-ui/core/InputLabel';

import purple from '@material-ui/core/colors/purple';
import green from '@material-ui/core/colors/green';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';

import themeBuilder from '../themes/DefaultTheme'

const DefaultTheme = themeBuilder();

const useStyles = makeStyles({
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
  button: {
    justifyContent: 'center'
  },
  card: {
    backgroundColor: DefaultTheme.palette.background.default,
    color: DefaultTheme.palette.primary.contrastText,
    minWidth: 275,
    maxWidth: 600
  }
});

export default function SelectCamera() {
  const classes = useStyles();
  


  const [state, setState] = React.useState({
    camera: '',
    name: 'hai',
  });

  const handleChange = (event) => {
    setState({
      ...state,
    });
  };

  return (
    <ThemeProvider theme={DefaultTheme}>
         <Card className={classes.card} variant="outlined" color='primary'>
            <CardContent>
                <Typography variant="h5" component="h2" color='textPrimary'>
                  Select Camera to Command:
                </Typography>

                <FormControl className={classes.formControl}>
                <Select
                native
                value={state.age}
                onChange={handleChange}
                inputProps={{
                    name: 'camera',
                    id: 'age-native-simple',
                }}
                >
                  <option >Camera 1</option>
                  <option >Camera 2</option>
                  <option >Camera 3</option>
                </Select>
            </FormControl>

            </CardContent>
            <CardActions className={classes.button}>
                <Button size="small" color='primary' variant='contained'>Select Camera</Button>
            </CardActions>
        </Card>
    </ThemeProvider>
  );
}