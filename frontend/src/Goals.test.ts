import {expect, test} from 'vitest';
import {render, screen} from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import Goals from './Goals.svelte';
import Dashboard from './Dashboard.svelte';
import Home from './Goals.svelte';
import Meals from './Meals.svelte';


test('Goals', async () => {
  render(Goals);
});

test('Dashboard', async () => {
  render(Dashboard);
});

test('Home', async () => {
  render(Home);
});

test('Meals', async () => {
  render(Meals);
});

test('BMR Calculation', async () => {
    render(Goals);

    await userEvent.type(screen.getByLabelText('Age'), '25');
    await userEvent.type(screen.getByLabelText('Gender'), 'F');
    await userEvent.type(screen.getByLabelText('Height (ft)'), '5');
    await userEvent.type(screen.getByLabelText('Height (in)'), '5');
    await userEvent.type(screen.getByLabelText('Weight'), '130');
    await userEvent.type(screen.getByLabelText('Activity'), 'S');
    const calculateButton = screen.getByText('Calculate');
    await userEvent.click(calculateButton);

    const expectedBMR = (10* 59) + (6.25 * 165.1) - (5 * 25) -161;
    expect(await screen.findByText(new RegExp(expectedBMR.toFixed(0)))).toBeTruthy();
});


test('Sidebar', () => {
    render(Dashboard);
    expect(screen.getByText('Dashboard')).toBeTruthy();
    expect(screen.getByText('My Meals')).toBeTruthy();
    expect(screen.getByText('My Goals')).toBeTruthy();
    expect(screen.getByText('Logout')).toBeTruthy();
});

test('Dashboard', () => {
    render(Dashboard);
    expect(screen.getByText('Daily Progress')).toBeTruthy();
    expect(screen.getByText('Calories')).toBeTruthy();
    expect(screen.getByText('Protein')).toBeTruthy();
    expect(screen.getByText('Fat')).toBeTruthy();
    expect(screen.getByText('Carbohydrates')).toBeTruthy();
});

test('Meals', () => {
    render(Meals);
    expect(screen.getByText('My Meals')).toBeTruthy();
});


