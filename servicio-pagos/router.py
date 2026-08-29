from fastapi import APIRouter, HTTPException, status, Depends
from service import PaymentService
from repository import PaymentRepository
from schemas import PayResponse, PayCreate

# Creamos la variable que va a contener la direccion de la url 
router = APIRouter (prefix="/pagos", tags=["pagos", ]) 

# Funcion que prepara el PaymentService  
def get_service ()->PaymentService:
    repository = PaymentRepository ()
    return PaymentService(repository)


#endpoint que nos devuelve los pagos guardados
@router.get ("/",
    response_model= list[PayResponse],
    status_code=status.HTTP_200_OK
)
async def get_payments (service: PaymentService = Depends(get_service)):
    return await service.list_payments ()


#endpoint que nos devuelve el pago por id 
@router.get ("/{payment_id}",
    response_model=PayResponse,
    status_code=status.HTTP_200_OK
)
async def get_by_id (
    payment_id: int, 
    service:PaymentService = Depends (get_service)):
    try:
        payment = await service.get_payment_by_id (payment_id)

    except ValueError as error: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    if not payment:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail="payment not found"
        )

    return payment


#endpoint que crea el pago y guarda a la base de datos 
@router.post  ("/",
    response_model=PayResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_payment (
    payment:PayCreate, 
    service:PaymentService = Depends(get_service)):
    try:
        return await service.payment_create (payment)

    except ValueError as error:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= str (error)
        )
