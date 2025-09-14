# Locust Load Test with Taurus

This repository contains a Locust-based load test for the DBank demo application, configured to run with Taurus and integrated with BlazeMeter for cloud execution.

## Test Overview

The test performs the following user flow:
1. **Login**: Authenticates with DBank using username/password
2. **Get Transactions**: Retrieves transaction data for account 161739

## Files

- `locustfile.py` - Locust test script defining the user behavior
- `taurus.yml` - Taurus configuration for load test execution
- `.github/workflows/blazemeter-test.yml` - GitHub Actions workflow for automated testing

## Prerequisites

- Python 3.7+
- pip

## Installation

```bash
# Install required packages
pip install bzt locust
```

## Configuration

### Environment Variables

The test uses BlazeMeter secrets for secure credential management:

```bash
# Set the password as an environment variable
export BZM_SECRET_dbank_rgarcia_password="your_password_here"
```

**Note**: In BlazeMeter, this should be configured as a secret named `dbank_rgarcia_password` in your workspace.

## Running Tests

### Local Execution with Taurus

```bash
# Run the load test
bzt taurus.yml
```

This will:
- Start 20 concurrent users
- Ramp up over 5 minutes
- Run for 10 minutes
- Target `http://dbankdemo.com`

### Direct Locust Execution

```bash
# Run Locust directly
locust -f locustfile.py --host http://dbankdemo.com --users 20 --spawn-rate 4 --run-time 10m --headless
```

## Load Test Configuration

Current configuration in `taurus.yml`:
- **Concurrency**: 20 users
- **Ramp-up**: 5 minutes
- **Duration**: 10 minutes
- **Target**: http://dbankdemo.com
- **Pass/Fail Criteria**:
  - Average response time > 1500ms for 1 minute → Stop as failed
  - Failures > 1% for 1 minute → Stop as failed

## BlazeMeter Integration

### GitHub Actions

The repository includes a GitHub Actions workflow that automatically:
1. Uploads test files to BlazeMeter
2. Runs the load test
3. Provides test results

### Required Secrets

Configure these secrets in your GitHub repository:

- `BLAZEMETER_API_KEY` - Your BlazeMeter API key
- `BLAZEMETER_API_SECRET` - Your BlazeMeter API secret
- `BLAZEMETER_TEST_ID` - Your existing BlazeMeter test ID

### BlazeMeter Secrets

In your BlazeMeter workspace, create a secret named `dbank_rgarcia_password` with the actual password value. This will be automatically injected as `BZM_SECRET_dbank_rgarcia_password` during test execution.

## Test Results

Taurus generates comprehensive reports including:
- Console output with real-time metrics
- Final statistics with percentiles
- Pass/fail criteria evaluation
- Detailed logs and artifacts

Results are saved in timestamped directories (automatically ignored by git).

## Customization

### Modifying Load Profile

Edit `taurus.yml` to adjust:
- `concurrency`: Number of concurrent users
- `ramp-up`: Time to reach full load
- `hold-for`: Test duration

### Adding Test Scenarios

Extend `locustfile.py` to add new user behaviors:
- Add new `@task` methods
- Modify user flow sequences
- Adjust wait times between requests

### Changing Target Application

Update the `default-address` in `taurus.yml` and ensure the API endpoints in `locustfile.py` match your target application.

## Troubleshooting

### Missing Password Error

If you see `Missing required secret env var: BZM_SECRET_dbank_rgarcia_password`, ensure:
- Environment variable is set locally, or
- Secret is configured in BlazeMeter workspace

### Connection Issues

- Verify the target URL is accessible
- Check firewall/proxy settings
- Ensure the application is running

## References

- [Taurus Documentation](https://gettaurus.org/)
- [Locust Documentation](https://docs.locust.io/)
- [BlazeMeter GitHub Actions](https://help.blazemeter.com/docs/guide/integrations-github-actions-and-bzm-related-functions_.htm)
- [BlazeMeter Secrets](https://help.blazemeter.com/docs/guide/performance-advanced-secrets.htm)
