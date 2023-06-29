<?php 

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;

class ApiController extends AbstractController
{
    public function index(): Response
    {
        return $this->json([
            'message' => 'Welcome to the API!',
        ]);
    }
}