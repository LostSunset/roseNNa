module readTester

    USE derived_types
    USE activation_functions

    implicit none


    TYPE(linLayer), ALLOCATABLE, DIMENSION(:) :: linLayers
    TYPE(lstmLayer), ALLOCATABLE, DIMENSION(:) :: lstmLayers
    TYPE(convLayer), ALLOCATABLE, DIMENSION(:) :: convLayers
    TYPE(maxpoolLayer), ALLOCATABLE, DIMENSION(:) :: maxpoolLayers
    CHARACTER(len = 20) :: activation_func
    REAL, ALLOCATABLE, DIMENSION(:,:) :: weights
    REAL, ALLOCATABLE, DIMENSION(:,:,:) :: midWeights
    REAL, ALLOCATABLE, DIMENSION(:,:,:,:) :: largeWeights
    INTEGER :: w_dim1
    INTEGER :: w_dim2
    INTEGER :: w_dim3
    INTEGER :: w_dim4

    REAL, ALLOCATABLE, DIMENSION(:) :: biases

    ! INTEGER :: activation_func

    CHARACTER(LEN = 10) :: layerName

    INTEGER :: numLayers
    INTEGER :: i

    contains
    
    subroutine initialize()
        INTEGER :: Reason
        CHARACTER(len = 20), ALLOCATABLE, DIMENSION(:) :: name
        ALLOCATE(lstmLayers(0))
        ALLOCATE(linLayers(0))
        ALLOCATE(convLayers(0))
        ALLOCATE(maxpoolLayers(0))
        open(10, file = "onnxModel.txt")
        open(11, file = "onnxWeights.txt")

        read(10, *) numLayers
        
        readloop: DO i = 1, 10
            read(10, *, IOSTAT=Reason) layerName
            if (Reason < 0) then
                exit readloop
            end if
            if (layerName .eq.  "LSTM") then
                CALL read_lstm(10, 11)
            else if (layerName .eq. "Gemm") then
                CALL read_linear(10, 11)
            else if (layerName .eq. "conv") then
                CALL read_conv(10, 11)
            else if (layerName .eq. "maxpool") then
                CALL read_maxpool(10, 11)
            else if (layerName .eq. "Reshape") then
                CYCLE
            else if (layerName .eq. "Transpose") then
                cycle
            else if (layerName .eq. "Squeeze") then
                cycle
            end if


            
        END DO readloop

    end subroutine
    subroutine read_maxpool(file1, file2)
        INTEGER, INTENT(IN) :: file1
        INTEGER, INTENT(IN) :: file2
        TYPE(maxpoolLayer), ALLOCATABLE, DIMENSION(:) :: maxpool
        ALLOCATE(maxpool(1))
        read(file1, *) w_dim1 !==w_dim2
        maxpool(1)%kernel_size = w_dim1
        ! maxpool(1)%stride = w_dim2
        maxpoolLayers = [maxpoolLayers, maxpool]
        DEALLOCATE(maxpool)
    end subroutine
    subroutine read_conv(file1, file2)
        INTEGER, INTENT(IN) :: file1
        INTEGER, INTENT(IN) :: file2
        TYPE(convLayer), ALLOCATABLE, DIMENSION(:) :: conv
        ALLOCATE(conv(1))
        read(file1, *) w_dim1, w_dim2, w_dim3, w_dim4
        ALLOCATE(largeWeights(w_dim1, w_dim2, w_dim3, w_dim4))
        read(file2, *) largeWeights
        conv(1)%weights = largeWeights
        DEALLOCATE(largeWeights)
        

        
        read(file1, *) w_dim1
        ALLOCATE(biases(w_dim1))
        read(file2, *) biases
        conv(1)%biases = biases
        DEALLOCATE(biases)

        
        convLayers = [convLayers, conv]

        DEALLOCATE(conv)
    end subroutine

    subroutine read_lstm(file1, file2)
        INTEGER, INTENT(IN) :: file1
        INTEGER, INTENT(IN) :: file2
        TYPE(lstmLayer), ALLOCATABLE, DIMENSION(:) :: lstm
        ALLOCATE(lstm(1))
        read(file1, *) w_dim1, w_dim2, w_dim3
        ALLOCATE(midWeights(w_dim1,w_dim2,w_dim3))
        read(file2, *) midWeights
        lstm(1)%wih = midWeights
        DEALLOCATE(midWeights)
        
        read(file1, *) w_dim1, w_dim2, w_dim3
        ALLOCATE(midWeights(w_dim1,w_dim2,w_dim3))
        read(file2, *) midWeights
        lstm(1)%whh = midWeights
        DEALLOCATE(midWeights)
        

        read(file1, *) w_dim1
        ALLOCATE(biases(w_dim1))
        read(file2, *) biases
        lstm(1)%bih = biases
        DEALLOCATE(biases)

        read(file1, *) w_dim1
        ALLOCATE(biases(w_dim1))
        read(file2, *) biases
        lstm(1)%bhh = biases
        DEALLOCATE(biases)
        lstmLayers = [lstmLayers, lstm]
        DEALLOCATE(lstm)
    end subroutine

    subroutine read_linear(file1, file2)
        INTEGER, INTENT(IN) :: file1
        INTEGER, INTENT(IN) :: file2
        TYPE(linLayer), ALLOCATABLE,DIMENSION(:) :: lin

        ALLOCATE(lin(1))
        read(file1, *) w_dim1, w_dim2
        ALLOCATE(weights(w_dim1,w_dim2))
        read(file2, *) weights

        read(file1, *) w_dim1
        ALLOCATE(biases(w_dim1))
        read(file2, *) biases

        read(file1, *) activation_func

        if (activation_func .eq. "Relu") then
            lin(1)%fn_ptr => relu2d
        else if (activation_func .eq. "Sigmoid") then
            lin(1)%fn_ptr => sigmoid2d
        else if (activation_func .eq. "Tanh") then
            lin(1)%fn_ptr => tanhh2d
        end if

        lin(1)%weights = weights
        lin(1)%biases = biases

        DEALLOCATE(weights)
        DEALLOCATE(biases)
        linLayers = [linLayers, lin]
        DEALLOCATE(lin)
    end subroutine


        
end module

