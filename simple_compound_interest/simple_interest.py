import sys
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_pv (pv_in):
    try:
        pv = Decimal(pv_in)
        if pv < 0:
            raise ValueError("PV (present value) must be non-negative.")
        if pv.quantize(Decimal("0.01")) != pv:
            raise ValueError ("PV (present value) must have exactly 2 decimal places.")
        return pv
    except (InvalidOperation, ValueError):
        raise ValueError("Invalid PV (present value): must be a non-negative number with 2 decimal places.")
    
def validate_interest_rate (r_in):
    try:
        r = Decimal(r_in) 
        if not (Decimal("0") <= r <= Decimal("1")):
            raise ValueError("r (interest rate) must be between 0 and 1.")
        if r.quantize(Decimal("0.01")) != r:
            raise ValueError ("r (interest rate) must have exactly 2 decimal places.")
        return r
    except (InvalidOperation, ValueError):
        raise ValueError("Invalid r (interest rate): must be a number betwen 0 and 1 with 2 decimal places.")
    
def validate_term(n_in):
    try:
        n = int(n_in)
        if n <= 0:
            raise ValueError("n (number of years) must be a positive integer.")
        return n
    except ValueError:
        raise ValueError("Invalid n (number of years): must be a positive whole number.")

def calculate_fv (pv, r, n):
    fv = pv * (Decimal("1") + r * Decimal(n))
    return fv.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def main():
    if len(sys.argv) != 4:
        logging.error(f"Expected 3 arguments: PV (present value) (non-negative with 2 decimal places), " 
                      "r (interest rate) (0-1 with 2 decimal places), and n (number of years) (positive integer).\n"
                      f"Received {len(sys.argv)-1} arguments. Arguments passed: {sys.argv[1:]}")
        sys.exit(1)
    
    try:
        logging.info(f"Arguments entered: PV (present value) = {sys.argv[1]}, r (interest rate) = {sys.argv[2]}, n (number of years) = {sys.argv[3]}")

        pv = validate_pv(sys.argv[1])
        r = validate_interest_rate(sys.argv[2])
        n = validate_term(sys.argv[3])

        fv = calculate_fv(pv, r, n)

        logging.info(f"Future Value (FV): ${fv}")
    except ValueError as e:
        logging.error(e)
        sys.exit(1)

if __name__ == "__main__":
    main()